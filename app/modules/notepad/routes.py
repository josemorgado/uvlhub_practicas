from flask import render_template, redirect, url_for, flash 
from flask_login import login_required, current_user

from app.modules.notepad.forms import NotepadForm
from app.modules.notepad import notepad_bp
from app.modules.notepad.services import NotepadService

notepad_service = NotepadService()

'''
READ ALL
'''


@notepad_bp.route('/notepad', methods=['GET'])
@login_required
def index():
    # Mete el formulario
    form = NotepadForm()
    # Pide los notepads al servicio    
    notepads = notepad_service.get_all_by_user(current_user.id)
    # Renderiza la plantilla con los notepads y el formulario
    return render_template('notepad/index.html', notepads=notepads, form=form)


'''
CREATE
'''


@notepad_bp.route('/notepad/create', methods=['GET', 'POST'])
@login_required
def create_notepad():
    form = NotepadForm()
    if form.validate_on_submit():
        result = notepad_service.create(
            form.title.data,
            form.body.data,
            current_user.id)
        return notepad_service.handle_service_response(
            result=result,
            errors=form.errors,
            success_url_redirect='notepad.index',
            success_msg='Notepad created successfully!',
            error_template='notepad/create.html',
            form=form
        )
    return render_template('notepad/create.html', form=form)


'''
READ BY ID
'''


@notepad_bp.route('/notepad/<int:notepad_id>', methods=['GET'])
@login_required
def get_notepad(notepad_id):
    notepad = notepad_service.get_or_404(notepad_id)

    if notepad.user_id != current_user.id:
        flash('You are not authorized to view this notepad', 'error')
        return redirect(url_for('notepad.index'))

    return render_template('notepad/show.html', notepad=notepad)


'''
EDIT
'''


@notepad_bp.route('/notepad/edit/<int:notepad_id>', methods=['GET', 'POST'])
@login_required
def edit_notepad(notepad_id):
    # Pide el notepad al servicio
    notepad = notepad_service.get_or_404(notepad_id)
    # Verifica que el notepad pertenece al usuario actual
    if notepad.user_id != current_user.id:
        # Si no es del usuario, muestra un mensaje de error y redirige
        flash('You are not authorized to edit this notepad', 'error')
        # Redirige a la lista de notepads
        return redirect(url_for('notepad.index'))
    # Si es del usuario, crea el formulario con los datos del notepad
    form = NotepadForm(obj=notepad)
    # Si el formulario es enviado y es válido, actualiza el notepad
    if form.validate_on_submit():
        
        result = notepad_service.update(
            notepad_id,
            title=form.title.data,
            body=form.body.data
        )
        # Maneja la respuesta del servicio
        return notepad_service.handle_service_response(
            result=result,
            errors=form.errors,
            success_url_redirect='notepad.index',
            success_msg='Notepad updated successfully!',
            error_template='notepad/edit.html',
            form=form
        )
    # Si el formulario no es enviado o no es válido, renderiza la plantilla
    return render_template('notepad/edit.html', form=form, notepad=notepad)


'''
DELETE
'''


@notepad_bp.route('/notepad/delete/<int:notepad_id>', methods=['POST'])
@login_required
def delete_notepad(notepad_id):
    notepad = notepad_service.get_or_404(notepad_id)
    if notepad.user_id != current_user.id:
        flash('You are not authorized to delete this notepad', 'error')
        return redirect(url_for('notepad.index'))

    result = notepad_service.delete(notepad_id)
    if result:
        flash('Notepad deleted successfully!', 'success')
    else:
        flash('Error deleting notepad', 'error')
    
    return redirect(url_for('notepad.index'))
