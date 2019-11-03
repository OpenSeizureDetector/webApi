<?php
namespace App\Test\TestCase\Controller;

use App\Controller\UsersController;
use Cake\TestSuite\IntegrationTestTrait;
use Cake\TestSuite\TestCase;
use Cake\ORM\TableRegistry;

/**
 * App\Controller\UsersController Test Case
 *
 * @uses \App\Controller\UsersController
 */
class UsersControllerTest extends TestCase
{
    use IntegrationTestTrait;

    /**
     * Fixtures
     *
     * @var array
     */
    public $fixtures = [
        'app.Users',
        'app.Usertypes',
        'app.Wearers'
    ];

    public function authorise() {
        $this->authorise_user();
    }

    public function authorise_admin() {
        $this->configRequest([
            'environment' => [
                'PHP_AUTH_USER' => 'admin',
                'PHP_AUTH_PW' => 'admin_pw',
                'SERVER_NAME' => 'localhost'
            ]
        ]);
    }        

    public function authorise_analyst() {
        $this->configRequest([
            'environment' => [
                'PHP_AUTH_USER' => 'analyst',
                'PHP_AUTH_PW' => 'analyst_pw',
                'SERVER_NAME' => 'localhost'
            ]
        ]);
    }        

    public function authorise_user() {
        $this->configRequest([
            'environment' => [
                'PHP_AUTH_USER' => 'user',
                'PHP_AUTH_PW' => 'user_pw',
                'SERVER_NAME' => 'localhost'
            ]
        ]);
    }        

    public function unauthorise() {
        $this->configRequest([
            'environment' => [
                'PHP_AUTH_USER' => '',
                'PHP_AUTH_PW' => '',
                'SERVER_NAME' => 'localhost'
            ]
        ]);
    }        

    
    public function testIndex()
    {
        $this->unauthorise();
        $this->get('/users.json');
        $this->assertResponseError("Unauthorised request succeeded incorrectly");
        $this->authorise_admin();
        $this->get('/users.json');
        $this->assertResponseOK("Authorised Request Failed (Admin)");
        $this->authorise_analyst();
        $this->get('/users.json');
        $this->assertResponseOK("Authorised Request Failed (analyst)");
        $this->authorise_user();
        $this->get('/users.json');
        //echo(print_r($this->_response));
        $this->assertResponseOK("Authorised Request Failed (user)");

    }

    /**
     * Test view method
     *
     * @return void
     */
    public function testView()
    {
        $this->unauthorise();
        $this->get('/users/view/1.json');
        $this->assertResponseError("Unauthorised view request succeeded incorrectly");

        $this->authorise_user();
        $this->get('/users/view/3.json');
        $this->assertResponseOK("Authorised view of own user record Failed (user)");

        $this->authorise_user();
        $this->get('/users/view/4.json');
        $this->assertResponseError("Authorised view of other users' user record succeeded incorrectly (user)");

        $this->authorise_analyst();
        $this->get('/users/view/3.json');
        $this->assertResponseError("Authorised view of other users user record succeeded incorrectly (analyst)");

        $this->authorise_admin();
        $this->get('/users/view/3.json');
        $this->assertResponseOK("Authorised view of other users user record  Failed (admin)");
        
    }

    private function makeTestData($uniqid) {
        $data =
            [
                'uname' => $uniqid,
                'email' => 'user@example.com',
                'password' => '$2y$10$i7W.7sFkSquAoUa40Wf/UuCcn9Jq/X4kBls2gXplEXAEqlRgpQJ8W',  //'user_pw',
                'usertype_id' => 3,
                'created' => '2019-11-01 13:50:00',
                'modified' => '2019-11-01 13:50:00'
            ];
        return $data;
    }

    
    /**
     * Test add method
     *
     * @return void
     */
    public function testAdd()
    {
        // Try to add a record when we are unauthorised - should fail
        $this->unauthorise();
        $uniqid = uniqid();
        $data = $this->makeTestData($uniqid);
        $this->post('/users/add.json', $data);
        $this->assertResponseError("Add unauthorised POST request succeeded incorrectly");
        $users = TableRegistry::getTableLocator()->get('Users');
        $query = $users->find()->where(['uname' => $uniqid]);
        $this->assertEquals(0, $query->count(),"Record created incorrectly");

        // Try to add a record when we are authorised as a normal user - should fail
        $this->authorise_user();
        $uniqid = uniqid();
        $data = $this->makeTestData($uniqid);
        $this->post('/users/add.json', $data);
        //echo($this->_response);
        $this->assertResponseError("Add authorised POST request succeeded incorrectly (user)");
        $users = TableRegistry::getTableLocator()->get('Users');
        $query = $users->find()->where(['uname' => $uniqid]);
        $this->assertEquals(0, $query->count(),"Record created incorrectly");

        // Try to add a record when we are authorised as an analyst - should fail
        $this->authorise_analyst();
        $uniqid = uniqid();
        $data = $this->makeTestData($uniqid);
        $this->post('/users/add.json', $data);
        $this->assertResponseError("Add unauthorised POST request succeeded incorrectly (analyst)");
        $users = TableRegistry::getTableLocator()->get('Users');
        $query = $users->find()->where(['uname' => $uniqid]);
        $this->assertEquals(0, $query->count(),"Record created incorrectly");
        
        // Try to add a record when we are authorised as an admin user - should succeed
        $this->authorise_admin();
        $uniqid = uniqid();
        $data = $this->makeTestData($uniqid);
        $this->post('/users/add.json', $data);
        //echo(print_r($this->_response));
        $this->assertResponseOK("Add admin POST request failed");
        $users = TableRegistry::getTableLocator()->get('Users');
        //echo("data");
        //echo(print_r($data));
        //$query = $users->find('all');
        //foreach ($query as $row)
        //    echo($row['uname'].", ");
        //echo(print_r($result));
        $query = $users->find()->where(['uname' => $uniqid]);
        $this->assertEquals(1, $query->count(),"Record not created");
    }

    /**
     * Test edit method
     *
     * @return void
     */
    public function testEdit()
    {
        $this->unauthorise();
        $this->get('/users/edit/1.json');
        $this->assertResponseError("Unauthorised view request succeeded incorrectly");

        $this->authorise_admin();
        $data=$this->makeTestData("user");
        $this->post('/users/edit/3.json',$data);
        $this->assertResponseOK("Authorised edit of own user record Failed (admin)");

        $this->authorise_user();
        $data=$this->makeTestData("user");
        $this->post('/users/edit/3.json',$data);
        $this->assertResponseOK("Authorised edit of own user record Failed (user)");
        
    }

    /**
     * Test delete method
     *
     * @return void
     */
    public function testDelete()
    {
        $this->unauthorise();
        $this->get('/users/delete/1.json');
        $this->assertResponseError("Unauthorised delete request succeeded incorrectly");

        $this->authorise_user();
        $this->post('/users/delete/3.json');
        $this->assertResponseError("Authorised delete of own user record succeeded incorrectly (user)");

        $this->authorise_analyst();
        $this->post('/users/delete/3.json');
        $this->assertResponseError("Authorised delete of user record succeeded incorrectly (analyst)");

        $this->authorise_admin();
        $this->post('/users/delete/3.json');
        $this->assertResponseOK("Authorised delete user record Failed (admin)");
    }
}
