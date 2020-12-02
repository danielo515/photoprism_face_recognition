import { wire } from 'hyperhtml';
import { getStylesFromDomNode } from './getStylesFromDomNode';

const calculateFaceOffset = (locations, cropSize = 100) => {
    const { top, left, bottom, right } = locations;
    // Faces are always square
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
 * @param {import('./appState').Face} face
 */
export function FaceBubble(face) {
    const { id, url, locations } = face;
    const { offsetX, offsetY } = calculateFaceOffset(locations);
    const style = {
        'background-position-x': offsetX,
        'background-position-y': offsetY,
        'background-image': `url("${url}")`,
    };
    const view = wire(face)`
    <div class="crop-wrapper" data-id=${id}>
        <div
            class="crop-face"
            style=${style}
        >
        </div>
    </div>
    `;
    return view;
}
