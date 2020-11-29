import { wire } from 'hyperhtml';

/**
 *
 * @param {Object} params
 * @param {Function} params.onClick handler, if not provider event will be propagated
 * @param {string} params.label What the button text should be
 */
export default function Button({ onClick, label }) {
    const click = (e) => {
        if (!onClick) return; // allow the default event to happen
        e.preventDefault();
        onClick(e);
    };
    return wire()`<button class="button" onclick=${click}>${label}</button>`;
}
