import { Button } from '@westpac/ui/button';
import { Heading } from '@westpac/ui/heading';
import { Panel, PanelBody } from '@westpac/ui/panel';
import { ProgressBar } from '@westpac/ui/progress-bar';

export default function App() {
  return (
    <main className="mx-auto max-w-md p-4">
      <Heading brandHeading size={2}>Westpac Autopilot</Heading>
      <Panel heading="Money Found this year">
        <PanelBody>
          <Heading size={1}>$412</Heading>
          <ProgressBar value={60} />
          <Button look="primary" className="mt-4">See what Autopilot did</Button>
        </PanelBody>
      </Panel>
    </main>
  );
}
