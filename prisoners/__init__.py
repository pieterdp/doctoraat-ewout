from flask import Flask, render_template, request, flash, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import and_

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

DEBUG = False

from prisoners.views.forms import InitForm, MatchForm
from prisoners.modules.matcher import Matcher
from prisoners.models.compare import PrisonersCompare


@app.route('/')
@app.route('/index/')
@app.route('/index')
def v_index():
    return render_template('admin/index.html')


@app.route('/init/', methods=['GET', 'POST'])
def v_init():
    form = InitForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Remove all items in the PrisonersCompare table
        PrisonersCompare.query.delete()
        m = Matcher()
        flash('Table re-initialised.')
        return redirect(url_for('.v_init'))
    return render_template('admin/init.html', form=form)


@app.route('/match/list/')
def v_match_list():
    unmatched_prisoners_id = db.session.query(PrisonersCompare.id_gedetineerde) \
        .filter(PrisonersCompare.has_been_checked == 0).distinct().order_by(PrisonersCompare.id_gedetineerde.asc()) \
        .all()
    unmatched_prisoners = []
    for prisoner_id in unmatched_prisoners_id:
        unmatched_prisoners.append(PrisonersCompare.query
                                   .filter(PrisonersCompare.id_gedetineerde == prisoner_id.id_gedetineerde).first())
    if len(unmatched_prisoners) > 0:
        first_prisoner = unmatched_prisoners[0]
        return render_template('admin/list.html', unmatched_prisoners=unmatched_prisoners,
                               prisoner_id=first_prisoner.id_gedetineerde)
    else:
        flash('Alles gekoppeld!')
        return redirect(url_for('.v_index'))


@app.route('/match/compare/<int:prisoner_id>', methods=['POST', 'GET'])
def v_match_compare(prisoner_id):
    current_prisoner = PrisonersCompare.query.filter(and_(PrisonersCompare.has_been_checked == 0,
                                                          PrisonersCompare.id_gedetineerde == prisoner_id)).first()
    possible_matches = PrisonersCompare.query.filter(and_(PrisonersCompare.has_been_checked == 0,
                                                          PrisonersCompare.id_gedetineerde == prisoner_id,
                                                          PrisonersCompare.l_score > 0.5)) \
        .order_by(PrisonersCompare.l_score.desc()).all()
    if not current_prisoner:
        new_prisoner_id = prisoner_id + 1
        return redirect(url_for('.v_match_compare', prisoner_id=new_prisoner_id))
    if len(possible_matches) > 0:
        matches_choices = []
        for possible_match in possible_matches:
            match_string = '{0} {1} ({2}) (score: {3})'.format(possible_match.c_voornaam, possible_match.c_naam,
                                                               possible_match.c_geboortejaar, possible_match.l_score)
            matches_choices.append((possible_match.c_id_gedetineerde, match_string))
        form = MatchForm()
        form.matches.choices = matches_choices
    else:
        flash('Geen matches voor deze gevangene.')
        current_prisoner.has_been_checked = True
        for prisoner in PrisonersCompare.query.filter(PrisonersCompare.id_gedetineerde == prisoner_id).all():
            # All prisoners with this id - do this for all prisoners with this id, matches or not
            prisoner.has_been_checked = True
            db.session.commit()
        new_prisoner_id = prisoner_id + 1
        return redirect(url_for('.v_match_compare', prisoner_id=new_prisoner_id))
    if request.method == 'POST' and form.validate_on_submit():
        for prisoner in PrisonersCompare.query.filter(PrisonersCompare.id_gedetineerde == prisoner_id).all():
            # All prisoners with this id - do this for all prisoners with this id, matches or not
            prisoner.has_been_checked = True
            db.session.commit()
        selected_matches = form.matches.data
        # selected_matches = array met c_id_gedetineerde van matches
        # naar volgende
        current_prisoner.has_been_checked = True
        db.session.commit()
        for selected_match in selected_matches:
            # Hier nog fouten
            s_prisoner = PrisonersCompare.query.filter(and_(PrisonersCompare.c_id_gedetineerde == selected_match,
                                                            PrisonersCompare.id_gedetineerde == prisoner_id)).first()
            current_prisoner.matches.append(s_prisoner)
            db.session.commit()
            # Add has_been_checked to all PrisonersCompare for which PrisonersCompare.id_gedetineerde OR
            # c_id_gedetineerde = selected_match or prisoner_id
            for prisoner in PrisonersCompare.query.filter(PrisonersCompare.id_gedetineerde == selected_match).all():
                # All prisoners with the id of the match
                prisoner.has_been_checked = True
                db.session.commit()
            if DEBUG is True:
                for prisoner in PrisonersCompare.query.filter(and_(PrisonersCompare.c_id_gedetineerde == selected_match,
                                                                   PrisonersCompare.l_score > 0.5)).all():
                    # All prisoners that are compared to this match
                    prisoner.has_been_checked = True
                    db.session.commit()
                for prisoner in PrisonersCompare.query.filter(and_(PrisonersCompare.c_id_gedetineerde == prisoner_id,
                                                                   PrisonersCompare.l_score > 0.5)).all():
                    # All prisoners that are compared to this prisoner
                    prisoner.has_been_checked = True
                    db.session.commit()
        flash('Gevangene gematched.')
        new_prisoner_id = prisoner_id + 1
        return redirect(url_for('.v_match_compare', prisoner_id=new_prisoner_id))
    else:
        if not current_prisoner:
            flash('Deze gevangene bestaat niet.')
            return redirect(url_for('.v_index'))
        prisoner_string = '{0} {1} ({2})'.format(current_prisoner.Voornaam, current_prisoner.Naam,
                                                 current_prisoner.Geboortejaar)
        return render_template('admin/match.html', form=form, prisoner_id=prisoner_id, prisoner_string=prisoner_string)

##
# To create the definitive table, go back to Gedetineerde; we use Id_gedetineerde and PrisonersCompare does not have
# all the gedetineerden: only those that can be matched!
