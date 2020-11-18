import { bind } from 'hyperhtml';
const modalNode = document.getElementById('modal');

export default function Modal({ onClose, content, isOpen }) {
    return bind(modalNode)`
    <div class="modal-wrapper" >
        <div class="modal-wrapper-inner">
            <div class="modal-body ${isOpen ? '' : 'modal-closed'}">
            ${content}
            </div>
        </div>
    </div>
    `;
}
