from flask import Blueprint, request, render_template, session, redirect, url_for

from ..models.workshop import WorkshopModels
from ...utilities.responseHelpers import bad_request

# BLUEPRINT ================================================== Begin
workshop = Blueprint(
    name='workshop',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/workshop',
)
# BLUEPRINT ================================================== End


# WORKSHOP PAGE ============================================================ Begin
# GET http://127.0.0.1:5000/workshop/
@workshop.get('/')
def index():
    try:
        # if session.get('role') != 1:
        #     return redirect(url_for('dashboard.index'))

        return render_template(
            title='Profil Bengkel - POS Bengkel',
            template_name_or_list='workshop.html',
        )

    except Exception as e:
        return bad_request(str(e))
# WORKSHOP PAGE ============================================================ End


# GET WORKSHOP ============================================================ Begin
# GET http://127.0.0.1:5000/workshop/view
@workshop.get('/view')
def getWorkshop():
    try:
        response = WorkshopModels.view_workshop()

        return response

    except Exception as e:
        return bad_request(str(e))
# GET WORKSHOP ============================================================ End


# UPDATE WORKSHOP ============================================================ Begin
# POST http://127.0.0.1:5000/workshop/edit
@workshop.post('/edit')
def updateWorkshop():
    try:
        datas = request.form
        logo = request.files.get("logo")

        response = WorkshopModels.edit_workshop(datas, logo)

        return response

    except Exception as e:
        return bad_request(str(e))
# UPDATE WORKSHOP ============================================================ End