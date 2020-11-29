import { bind, wire } from 'hyperhtml';
const modalNode = document.getElementById('modal');
import './styles/modal.scss';

export default function Modal({ onClose, content, isOpen, title = null }) {
    return bind(modalNode)`
    <div class="modal-wrapper  ${isOpen ? '' : 'modal-closed'}" >
    ${title && wire(title, ':modal-title')`<h2 class="title">${title}</h2>`}
    <div class="modal-background" onClick=${onClose}/>
    <div class="modal-wrapper-inner">
        <div class="modal-body">
        ${content}
        </div>
    </div>
    </div>
    `;
}
