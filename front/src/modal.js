import { bind, wire } from 'hyperhtml';
const modalNode = document.getElementById('modal');
import './styles/modal.scss';

const render = bind(modalNode);

export default function Modal({ onClose, content, isOpen, title = null }) {
    return render`
    <div class="modal-wrapper  ${isOpen ? '' : 'modal-closed'}" >
    <div class="modal-background" onClick=${onClose}/>
    <div class="modal-wrapper-inner">
        <div class="modal-body">
        ${
            title &&
            wire(content, ':modal-title')`<h2 class="modal-title">${title}</h2>`
        }
        ${content}
        </div>
    </div>
    </div>
    `;
}
