import { FaceBubble } from './FaceBubble';
import { wire } from 'hyperhtml';
import './FacesList.scss';
import { toggleFace, isFaceSelected } from './appState';

/**
 *
 * @param {import('./FaceBubble').BubbleEvent} e
 */
const onBubbleClick = (e) => toggleFace(e.currentTarget.data);

/**
 *
 * @param {Object} param
 * @param {import('./appState').Face[]} param.faces
 * @param {string} [param.className]
 */
export function FacesList({ faces, className = '' }) {
    return wire()`
    <div class="faces-list ${className}">
        ${faces.map((face) =>
            FaceBubble({
                face,
                onClick: onBubbleClick,
                isSelected: isFaceSelected(face.id),
            }),
        )}
    </div>`;
}
