<?php
namespace App\Command;

use Cake\Console\Arguments;
use Cake\Console\Command;
use Cake\Console\ConsoleIo;
use Cake\Console\ConsoleOptionParser;
use Cake\ORM\TableRegistry;

/**
 * CreateUser command.
 */
class CreateUserCommand extends Command
{
    public function initialize()
    {
        parent::initialize();
        $this->loadModel('Users');
    }
    
    public function buildOptionParser(ConsoleOptionParser $parser)
    {
        $parser = parent::buildOptionParser($parser);
        $parser->addOption('uname', [
            'help' => 'User Name:'
        ]);
        $parser->addOption('email', [
            'help' => 'Email:'
        ]);
        $parser->addOption('password', [
            'help' => 'Password:'
        ]);

        return $parser;
    }

    /**
     * Implement this method with your command's logic.
     *
     * @param \Cake\Console\Arguments $args The command arguments.
     * @param \Cake\Console\ConsoleIo $io The console io
     * @return null|int The exit code or null for success
     */
    public function execute(Arguments $args, ConsoleIo $io)
    {
        $uname = $args->getOption('uname');
        $email = $args->getOption('email');
        $password = $args->getOption('password');

        $err=0;
        if ($uname=="") {
            $io->out("ERROR - must specify user name");
            $err=1;
        }
        if ($email=="") {
            $io->out("ERROR - must specify email");
            $err=1;
        }
        if ($password=="") {
            $io->out("ERROR - must specify password");
            $err=1;
        }
        if ($err!=0)
            $io->out("Error(s) in input data - not doing anything");
        else {
            $io->out("Creating user {$uname} with email {$email} and password {$password}.");
            $userTable = TableRegistry::get('Users');
            $exists = $userTable->exists(['uname' => $uname]);
            if ($exists) {
                $io->out("ERROR: User {$uname} already exists");
            }
            else {
                $io->out("OK - user {$uname} does not exist yet");
                $user = $this->Users->newEntity();
                $user->uname=$uname;
                $user->email=$email;
                $user->password=$password;
                if ($this->Users->save($user)) {
                    $io->out("User Saved OK");
                    $user = $this->Users->findByUname($uname)->first();
                    $io->out(print_r($user, true));
                } else {
                    $io->out("ERROR Saving User");
                }
            }
        }
    }
}
