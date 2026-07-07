from flask import Blueprint, request, render_template, session, redirect, url_for


from ..models.customer import CustomerModels
from ...utilities.responseHelper import bad_request

# BLUEPRINT ================================================== Begin
customer = Blueprint(
    name='customer',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/customer',
)
# BLUEPRINT ================================================== End


# CUSTOMER PAGE ============================================================ Begin
# [GET] https://127.0.0.1:5000/customer/
@customer.get('/')
def index():
    try:
        if 'user_id' not in session:
            return redirect(url_for('auth.signin_page'))

        if session.get('role') != 1:
            return redirect(url_for('dashboard.index'))

        return render_template(
            title='Customer - POS Bengkel',
            template_name_or_list='customer.html',
            active_menu="customer",
        )
    except Exception as e:
        return bad_request(str(e))
# CUSTOMER PAGE ============================================================ End


# ADD CUSTOMER DATA ============================================================ Begin
# [POST] https://127.0.0.1:5000/customer/add
@customer.post('/add')
def create_customer():
    try:

        body = request.json

        response = CustomerModels.add_customer(body)

        return response

    except Exception as e:
        return bad_request(str(e))
# ADD CUSTOMER DATA ============================================================ End

# GET CUSTOMER DATA ============================================================ Begin
# GET https://127.0.0.1:5000/customer/view
@customer.get('/view')
def get_customer():
    try:

        response = CustomerModels.view_customer()

        return response

    except Exception as e:
        return bad_request(str(e))
# GET CUSTOMER DATA ============================================================ End


# UPDATE CUSTOMER DATA ============================================================ Begin
# [PUT] https://127.0.0.1:5000/customer/edit/<id>
@customer.put('/edit/<int:id>')
def update_customer(id):
    try:

        body = request.json

        response = CustomerModels.edit_customer(body, id)

        return response

    except Exception as e:
        return bad_request(str(e))
# UPDATE CUSTOMER DATA ============================================================ End


# DELETE CUSTOMER DATA ============================================================ Begin
# [DELETE] https://127.0.0.1:5000/customer/delete/<id>
@customer.delete('/delete/<int:id>')
def delete_customer(id):
    try:

        response = CustomerModels.delete_customer(id)

        return response

    except Exception as e:
        return bad_request(str(e))
# DELETE CUSTOMER DATA ============================================================ End