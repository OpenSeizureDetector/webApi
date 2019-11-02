<?php
namespace App\Test\Fixture;

use Cake\TestSuite\Fixture\TestFixture;

/**
 * UsersFixture
 */
class UsersFixture extends TestFixture
{
    public $import = ['table' => 'users'];
    public function init() {
        $this->records = [
            [
                'id' => 1,
                'uname' => 'admin',
                'email' => 'admin@example.com',
                'password' => '$2y$10$WN2jByiqJZE25uGM8Kl17.OTfKPZBVNB/sx69p7si5oDSz01xv3Vi',  //'admin_pw',
                'usertype_id' => 1,
                'created' => '2019-11-01 13:50:00',
                'modified' => '2019-11-01 13:50:00'
            ],
            [
                'id' => 2,
                'uname' => 'analyst',
                'email' => 'analyst@example.com',
                'password' => '$2y$10$OpYQIl8y0fKtDgNSBw7Q..1aPLWuSwWOINc7HFyC.45Alvt24B6IC',  //'analyst_pw',
                'usertype_id' => 2,
                'created' => '2019-11-01 13:50:00',
                'modified' => '2019-11-01 13:50:00'
            ],
            [
                'id' => 3,
                'uname' => 'user',
                'email' => 'user@example.com',
                'password' => '$2y$10$i7W.7sFkSquAoUa40Wf/UuCcn9Jq/X4kBls2gXplEXAEqlRgpQJ8W',  //'user_pw',
                'usertype_id' => 3,
                'created' => '2019-11-01 13:50:00',
                'modified' => '2019-11-01 13:50:00'
            ],
        ];
        parent::init();
    }
}
