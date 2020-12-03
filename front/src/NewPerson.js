import { wire } from 'hyperhtml';
import Button from './Button';
import Input from './Input';
import Modal from './Modal';
import { createPerson, getFaceMatches } from './api';
import './styles/new-person.scss';
import { removeSelection } from './actions';
import { FacesList } from './FacesList';

const closeModal = () =>
    Modal({ content: null, isOpen: false, onClose: () => {} });

/**
 *
 * @param {Object} props
 * @param {import('./appState').Face[]} props.faces The face to assign to the new person
 * @param {boolean} props.isOpen if the modal should be open
 */
export default function NewPerson({ faces, isOpen }) {
    const state = { value: '' };
    const save = (e) => {
        const faceIds = faces.map((x) => x.id);
        e.preventDefault();
        createPerson({ name: state.value, faces: faceIds })
            .then(() => {
                removeSelection(faceIds);
                closeModal();
            })
            .catch(() => alert('Woops, failed'));
    };
    const onBlur = (value) => (state.value = value);
    const body = wire(faces)`
    <div class="new-person" >
    <div class="top-section">
        <img src="${faces[0].url}" alt="new-person-picture"/>
        <form onsubmit=${save}>
            <div class="form-row">
                ${Input({
                    label: 'Person Name',
                    name: 'person-name',
                    onBlur,
                    onChange: onBlur,
                })}
            </div>
            <div class="form-row">
                ${Button({
                    label: 'Save',
                    onClick: save,
                })}
            </div>
        </form>
    </div>
        
    <div class="bottom-section">
        <h3>Faces that will be assigned</h3>
            ${FacesList({ faces, className: 'faces-list' })}
    </div>

        ${getFaceMatches({ id: faces[0].id }).then(({ faces }) =>
            FacesList({ faces, className: 'new-person-suggestions' }),
        )}
        
    </div>
    `;
    return Modal({
        content: body,
        isOpen,
        title: 'Create new person',
        onClose: closeModal,
    });
}
