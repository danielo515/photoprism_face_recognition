import { wire } from 'hyperhtml';

export default function Button({ onClick, label }) {
    return wire()`<button class="button" onclick=${onClick}>${label}</button>`;
}
