import { wire } from 'hyperhtml';
import Button from './Button';
import Input from './Input';
import Modal from './modal';
import './styles/new-person.scss';

export default function NewPerson({ face, isOpen }) {
    const state = { value: '' };
    const save = (e) => e.preventDefault() && console.log(state);
    const onBlur = (value) => (state.value = value);
    const body = wire()`
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
               onClick: () => console.log(state),
           })}</div>
        </form>
    </div>
    `;
    return Modal({ content: body, isOpen });
}
