import { wire } from 'hyperhtml';

export default function newUserBtn({ onClick }) {
    return wire()`
    <button class="btn-icon" aria-label="Create new person and assign faces" onClick=${onClick}>
        <li class="fas fa-user-plus"></li>
    </button>
    `;
}
