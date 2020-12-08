import { FaceBubble } from './FaceBubble';
import { wire } from 'hyperhtml';
import './FacesList.scss';
import { toggleFace, isFaceSelected } from './appState';

/**
 *
 * @param {import('./FaceBubble').BubbleEvent} e
 */
const onBubbleClick = (render) => (e) => {
    toggleFace(e.currentTarget.data);
    render();
};

/**
 *
 * @param {Object} props
 * @param {import('./appState').Face[]} props.faces
 * @param {string} [props.className]
 */
export function FacesList(props) {
    const { faces, className = '' } = props;
    return wire(faces, ':faces-list')`
    <div class="faces-list ${className}">
        ${faces.map((face) =>
            FaceBubble({
                face,
                onClick: onBubbleClick(() => FacesList(props)),
                isSelected: isFaceSelected(face.id),
            }),
        )}
    </div>`;
}
