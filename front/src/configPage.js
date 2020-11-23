import { bind } from 'hyperhtml';
import Button from './Button';

export default function ConfigPage(rootNode, state = {}) {
    const { scan_status } = state;
    const canStartScan = ['not_started', 'finished'].includes(scan_status);
    const buttonLabel =
        scan_status === 'not_started' ? 'Start scan' : 'Re-scan';
    const onClick = () => ConfigPage(rootNode, { scan_status: 'in_progress' });
    return bind(rootNode)`
    <div>
        ${canStartScan ? Button({ onClick: onClick, label: buttonLabel }) : ''}
    </div>
    `;
}
