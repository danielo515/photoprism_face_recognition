import { wire } from 'hyperhtml';
import './styles/face-bubble.scss';

const calculateFaceOffset = (locations, cropSize = 100) => {
    const { top, left, bottom, right } = locations;
    // assume square face
    const faceSize = right - left;
    const offset = cropSize - faceSize;
    const leftX = Math.max(left - offset - 2, 0);
    const offsetY = Math.max(top - offset - 2, 0);

    return {
        offsetX: Math.min(leftX, cropSize) + '%',
        offsetY: Math.min(offsetY, cropSize) + '%',
    };
};

/**
 *
 * @typedef BubbleEvent
 * @property {Object} currentTarget
 * @property {import('./appState').Face} currentTarget.data
 * @property {object} currentTarget.classList
 * @property {function} currentTarget.classList.toggle
 */
/**
 *
 * @param {Object} params
 * @param {boolean} [ params.isSelected ]
 * @param {(e:BubbleEvent) => void} [ params.onClick ]
 * @param {import('./appState').Face} params.face
 */
export function FaceBubble({ face, isSelected = false, onClick }) {
    const { id, url, locations } = face;
    const { offsetX, offsetY } = calculateFaceOffset(locations);
    const style = {
        'background-position-x': offsetX,
        'background-position-y': offsetY,
        'background-image': `url("${url}")`,
    };
    const view = wire(face)`
    <div class="crop-wrapper" data=${face} data-id=${id} onclick=${onClick}>
        <div
            class="crop-face ${isSelected ? 'selected' : ''}"
            style=${style}
        >
        </div>
    </div>
    `;
    return view;
}
