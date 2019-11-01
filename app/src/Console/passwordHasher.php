namespace App\Command;

use Cake\Console\Arguments;
use Cake\Console\Command;
use Cake\Console\ConsoleIo;
use Cake\Console\ConsoleOptionParser;

class HelloCommand extends Command
{
    protected function buildOptionParser(ConsoleOptionParser $parser)
    {
        $parser->addArgument('name', [
            'help' => 'What is your name'
        ]);
        return $parser;
    }

    public function execute(Arguments $args, ConsoleIo $io)
    {
        $name = $args->getArgument('name');
        $io->out("Hello {$name}.");
    }
}