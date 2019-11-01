<?php
namespace App\Command;

use Cake\Console\Arguments;
use Cake\Console\Command;
use Cake\Console\ConsoleIo;
use Cake\Console\ConsoleOptionParser;
use Cake\ORM\TableRegistry;

/**
 * Password command.
 */
class PasswordCommand extends Command
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
        $parser->addOption('password', [
            'help' => 'Password:'
        ]);
        $parser->addOption('auto', [
            'help' => 'Automatically Generate Password:',
            'boolean' => true
        ]);

        return $parser;
    }


// From https://stackoverflow.com/questions/6101956/generating-a-random-password-in-php
    public function randomPassword($pwdLen=8) {
        $alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!_()@';
        $pass = array(); //remember to declare $pass as an array
        $alphaLength = strlen($alphabet) - 1; //put the length -1 in cache
        for ($i = 0; $i < $pwdLen; $i++) {
            $n = rand(0, $alphaLength);
            $pass[] = $alphabet[$n];
        }
        return implode($pass); //turn the array into a string
    }

    
    public function execute(Arguments $args, ConsoleIo $io)
    {
        $uname = $args->getOption('uname');
        $password = $args->getOption('password');
        $auto = $args->getOption('auto');
        $io->out("auto= {$auto}");
        $err=0;
        if ($uname=="") {
            $io->out("ERROR - must specify user name");
            $err=1;
        }
        if ($password=="" and $auto!=True) {
            $io->out("ERROR - must specify password or auto");
            $err=1;
        }
        if ($err!=0) {
            $io->out("Error(s) in input data - not doing anything");
            $this->abort();
        }

        $userTable = TableRegistry::get('Users');
        $exists = $userTable->exists(['uname' => $uname]);
        if (!$exists) {
            $io->out("ERROR: User {$uname} does not exist");
            $this->abort();
        }

        if ($auto==True) {
            $password=$this->randomPassword(8);
            $io->out("Generated Random Password {$password}");
        } else {
            $io->out("Auto is false");
        }

        $user = $this->Users->findByUname($uname)->first();
        $user->password=$password;

        $io->out("uname={$user->uname}");
        $io->out("password={$password}, {$user->password}");
        if ($this->Users->save($user)) {
            $io->out("User Saved OK");
        } else {
            $io->out("ERROR Saving User");
        }
    }

}
