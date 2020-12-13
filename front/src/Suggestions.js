import { wire } from 'hyperhtml';
import Button from './Button';
import { FacesList } from './FacesList';
import './styles/suggestions.scss';
import { addFaces } from './appState';

export const Suggestions = ({ faces }) => wire(faces, ':suggestions')`
        <div class="face-suggestions">
            <h3>Select other possible matches</h3>
            ${Button({
                onClick: () => {
                    addFaces(faces);
                    Suggestions({ faces });
                },
                label: 'Select all',
            })}</div>
            ${FacesList({ faces, className: 'new-person-suggestions' })}
        `;
