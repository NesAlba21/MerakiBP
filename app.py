import meraki
from prettytable import PrettyTable
from flask import session
from flask import Flask, render_template, flash, url_for, session, redirect, send_file, after_this_request
from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField
from wtforms.validators import DataRequired
import os

from MerakiHealthCheckWeb import create_document

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cisco'



@app.route('/', methods=['GET', 'POST']) #127.0.0.1:5000
def index():
    #Check if a file exist and delete it
    fp = 'Meraki Health Check.docx'
    if os.path.isfile(fp):
        os.remove(fp)
        print(f"{fp} deleted")
    else:
        print("File not found")

    class apiForm(FlaskForm):
        api = StringField("Please enter your Meraki API key: ", validators=[DataRequired()], render_kw={"class": "form-control"})
        submit = SubmitField('Submit', render_kw={"class": "btn btn-success w-100"})
    form = apiForm()
    if form.validate_on_submit():
        session['api'] = form.api.data
        return redirect(url_for('orgs'))
    else:
        if 'api' in session:
            return redirect(url_for('orgs'))

        return render_template('index.html', form=form)

@app.route('/orgs', methods = ['GET', 'POST'])
def orgs():
    if 'api' in session:
        api = session['api']
        dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)
        response = dashboard.organizations.getOrganizations()
        list_data = []
        for data in response:
            orgName = (data['name'])
            orgId = (data['id'])
            list_Temp = (orgId, orgName)
            list_data.append(list_Temp)
        list_data.sort()



        class OrgForm(FlaskForm):
            org = RadioField('Please choose a desire organization', choices=list_data, validators=[DataRequired()])
            submit = SubmitField('Next', render_kw={"class": "btn btn-success w-100"})
        form = OrgForm()
        print(form.validate_on_submit())
        if form.validate_on_submit():
            print(form.validate_on_submit())
            session['orgs'] = form.org.data
            return redirect(url_for('networks'))

        return render_template('orgs.html', list_data=list_data, form=form)
    else:
        return redirect(url_for('logout'))

@app.route('/networks', methods=['GET', 'POST'])
def networks():
    if 'api' and 'orgs' in session:
        api = session['api']
        orgId = session['orgs']
        dashboard = meraki.DashboardAPI(api, print_console=False, output_log=False)
        response = dashboard.organizations.getOrganizationNetworks(orgId, total_pages='all')
        list_data = []
        list_data.sort()
        for data in response:
            networkName = (data['name'])
            netId = (data['id'])
            list_Temp = (netId, networkName)
            list_data.append(list_Temp)
        list_data.sort()

        class NetworksForm(FlaskForm):
            networks = RadioField('Please choose a desire network', choices=list_data, validators=[DataRequired()])
            submit = SubmitField('Next', render_kw={"class": "btn btn-success w-100"})
        form = NetworksForm()
        if form.validate_on_submit():
            session['networks'] = form.networks.data
            selected_option = form.networks.data
            print(selected_option)
            return redirect(url_for('report'))

        return  render_template('networks.html', orgId=orgId, form=form)
    else:
        return redirect(url_for('logout'))

@app.route('/report', methods=['GET','POST'])
def report():
    if 'api' and 'orgs' and 'networks' in session:
        return render_template('report.html')
    else:
        return redirect(url_for('logout'))


@app.route('/download', methods=['GET','POST'])
def download_report():
    if 'api' and 'orgs' and 'networks' in session:
        api = session['api']
        network_id = session['networks']
        orgId = session['orgs']

        create_document(api, orgId, network_id)


        p = 'Meraki Health Check.docx'
        return send_file(p, as_attachment=True)
    else:
        return redirect(url_for('logout'))


@app.route('/logout')
def logout():
    session.pop('api', None)
    session.pop('orgs', None)
    session.pop('networks', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
