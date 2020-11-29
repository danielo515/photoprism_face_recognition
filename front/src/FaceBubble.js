import { wire } from 'hyperhtml';
import { getStylesFromDomNode } from './getStylesFromDomNode';

/**
 *
 * @param {import('./appState').Face} face
 */
export function FaceBubble(face) {
    const { id } = face;
    const style = getStylesFromDomNode(id);
    const view = wire(face)`
    <div class="crop-wrapper">
        <div
            class="crop-face"
            style=${style}
        >
        </div>
    </div>
    `;
    return view;
}
