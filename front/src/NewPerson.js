import { wire } from 'hyperhtml';
import Button from './Button';
import Input from './Input';
import Modal from './modal';
import { createPerson } from './api';
import './styles/new-person.scss';
import { removeFacesFromDOM } from './App';
import { clearFaces } from './appState';

const closeModal = () =>
    Modal({ content: null, isOpen: false, onClose: () => {} });

/**
 *
 * @param {Object} props
 * @param {{id: string, url: string}} props.face The face to assign to the new person
 * @param {boolean} props.isOpen if the modal should be open
 */
export default function NewPerson({ face, isOpen }) {
    const state = { value: '' };
    const save = (e) => {
        e.preventDefault();
        createPerson({ name: state.value, faces: [face.id] }).then(() => {
            removeFacesFromDOM([face.id]);
            clearFaces();
            closeModal();
        });
    };
    const onBlur = (value) => (state.value = value);
    const body = wire(face)`
    <div class="new-person" >
        <img src="${face.url}" alt="new-person-picture"/>
        <form onsubmit=${save}>
            <div class="form-row">
                ${Input({
                    label: 'Person Name',
                    name: 'person-name',
                    onBlur,
                    onChange: onBlur,
                })}
            </div>
           <div class="form-row"> ${Button({
               label: 'Save',
               onClick: save,
           })}</div>
        </form>
    </div>
    `;
    return Modal({
        content: body,
        isOpen,
        onClose: closeModal,
    });
}
