import { wire } from 'hyperhtml';

export default function ButtonIcon({ onClick, label, icon }) {
    return wire()`
    <button class="button btn-icon" aria-label=${label} onClick=${onClick}>
        <li class="fas fa-${icon}"></li>${label}
    </button>
    `;
}
