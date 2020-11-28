import ButtonIcon from './ButtonIcon';
import { clearSelection } from './App';
import { appState } from './appState';
import { assignSelectedFacesToPerson } from './api';
import { wire, bind } from 'hyperhtml';
import NewPerson from './NewPerson';

export const toolbar = () => {
    const toolbarDom = document.getElementById('toolbar');
    const options = wire(appState, ':people-options')`${server_data.people.map(
        (item) => wire(item, ':option')`
        <option value=${item.id}>
            ${item.name}
        </option>
        `,
    )}
    `;
    bind(toolbarDom)`
    <button class="button" onClick=${() =>
        assignSelectedFacesToPerson({
            person_id: appState.selectedPerson,
        })}>Assign selection to: </button>
    <select onchange=${(e) => (appState.selectedPerson = e.target.value)}>
        <option hidden selected> Select a person</option>
        ${options}
    </select>
    ${ButtonIcon({
        label: 'Create new person',
        icon: 'user-plus',
        onClick: NewPerson({
            faceId: appState.selectedFaces.values().next().value,
            isOpen: true,
        }),
    })}
    <button onClick=${clearSelection}>clear selection</button>
    `;
    if (appState.selectedFaces.size > 0)
        toolbarDom.classList.add('toolbar-show');
    else toolbarDom.classList.remove('toolbar-show');
};
