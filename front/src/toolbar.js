import './styles/toolbar.scss';
import ButtonIcon from './ButtonIcon';
import { clearSelection } from './App';
import * as State from './appState';
import { wire, bind } from 'hyperhtml';
import NewPerson from './NewPerson';
import Button from './Button';

const select = () => {
    const options = wire(
        State.appState,
        ':people-options',
    )`${window.server_data.people.map(
        (item) => wire(item, ':option')`
        <option value=${item.id}>
            ${item.name}
        </option>
        `,
    )}
    `;
    return `<select onchange=${(e) =>
        (State.appState.selectedPerson = e.target.value)}>
        <option hidden selected> Select a person</option>
        ${options}
    </select>
`;
};

export const toolbar = () => {
    const toolbarDom = document.getElementById('toolbar');
    bind(toolbarDom)`
    ${ButtonIcon({
        label: 'Create new person',
        icon: 'user-plus',
        onClick: () =>
            NewPerson({
                face: State.getFirstFace(),
                isOpen: true,
            }),
    })}
    ${Button({ onClick: clearSelection, label: 'Clear selection' })}
    `;
    if (State.facesCount() > 0) toolbarDom.classList.add('toolbar-show');
    else toolbarDom.classList.remove('toolbar-show');
};
