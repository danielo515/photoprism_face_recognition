import { bind } from 'hyperhtml';
const modalNode = document.getElementById('modal');
import './styles/modal.scss';

export default function Modal({ onClose, content, isOpen }) {
    return bind(modalNode)`
    <div class="modal-wrapper  ${isOpen ? '' : 'modal-closed'}" >
        <div class="modal-wrapper-inner">
            <div class="modal-body">
            ${content}
            </div>
        </div>
    </div>
    `;
}
