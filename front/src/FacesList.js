import { FaceBubble } from './FaceBubble';
import { wire } from 'hyperhtml';
import './FacesList.scss';

/**
 *
 * @param {Object} param
 * @param {import('./appState').Face[]} param.faces
 * @param {string} param.className
 */
export function FacesList({ faces, className = '' }) {
    return wire()`
    <div class="faces-list ${className}">
        ${faces.map((face) => FaceBubble(face))}
    </div>`;
}