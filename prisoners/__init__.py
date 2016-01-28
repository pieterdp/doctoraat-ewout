from flask import Flask, render_template, request, flash, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

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
    unmatched_prisoners = PrisonersCompare.query.filter(PrisonersCompare.has_been_checked == 0) \
        .order_by(PrisonersCompare.id_gedetineerde.asc()).all()
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
                                                          PrisonersCompare.l_score > 0.5)).all()
    matches_choices = []
    for possible_match in possible_matches:
        match_string = '{0} {1} ({2}-{3}-{4}) (score: {5})'.format(possible_match.c_voornaam, possible_match.c_naam,
                                                      possible_match.c_geboortedag, possible_match.c_geboortemaand,
                                                      possible_match.c_geboortejaar, possible_match.l_score)
        matches_choices.append((possible_match.c_id_gedetineerde, match_string))
    form = MatchForm()
    form.matches.choices = matches_choices
    if request.method == 'POST' and form.validate_on_submit():
        selected_matches = form.matches.data
        print(selected_matches)
        # selected_matches = array met c_id_gedetineerde van matches
        # naar volgende
        flash('test')
    else:
        if not current_prisoner:
            flash('Deze gevangene bestaat niet.')
            return redirect(url_for('.v_index'))
        prisoner_string = '{0} {1} ({2}-{3}-{4})'.format(current_prisoner.Voornaam, current_prisoner.Naam,
                                                         current_prisoner.Geboortedag, current_prisoner.Geboortemaand,
                                                         current_prisoner.Geboortejaar)
        return render_template('admin/match.html', form=form, prisoner_id=prisoner_id, prisoner_string=prisoner_string)
