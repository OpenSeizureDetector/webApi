<?php
namespace App\Test\TestCase\Controller;

use App\Controller\WearersController;
use Cake\TestSuite\IntegrationTestTrait;
use Cake\TestSuite\TestCase;
use Cake\ORM\TableRegistry;

class WearersControllerTest extends TestCase
{
    use IntegrationTestTrait;

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
        $this->get('/wearers.json');
        $this->assertResponseError("Unauthorised request succeeded incorrectly");
        $this->authorise_admin();
        $this->get('/wearers.json');
        $this->assertResponseOK("Authorised Request Failed (Admin)");
        $this->authorise_analyst();
        $this->get('/wearers.json');
        $this->assertResponseOK("Authorised Request Failed (analyst)");
        $this->authorise_user();
        $this->get('/wearers.json');
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
        $this->get('/wearers/view/1.json');
        $this->assertResponseError("Unauthorised view request succeeded incorrectly");

        $this->authorise_user();
        $this->get('/wearers/view/3.json');
        $this->assertResponseOK("Authorised view of own wearer record Failed (user)");

        $this->authorise_user();
        $this->get('/wearers/view/4.json');
        $this->assertResponseError("Authorised view of other users' wearer record succeeded incorrectly (user)");

        $this->authorise_analyst();
        $this->get('/wearers/view/3.json');
        $this->assertResponseError("Authorised view of other users wearer record succeeded incorrectly (analyst)");

        $this->authorise_admin();
        $this->get('/wearers/view/3.json');
        $this->assertResponseOK("Authorised view of other users wearer record  Failed (admin)");
        
    }

    private function makeTestData($uniqid) {
        $data = [
                'name' => $uniqid,
                'dob' => '2019-11-02',
                'ald' => 1,
                'user_id' => 3,
                'created' => '2019-11-02 19:29:58',
                'modified' => '2019-11-02 19:29:58'
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
        $this->post('/wearers/add.json', $data);
        $this->assertResponseError("Add unauthorised POST request succeeded incorrectly");
        $wearers = TableRegistry::getTableLocator()->get('Wearers');
        $query = $wearers->find()->where(['name' => $uniqid]);
        $this->assertEquals(0, $query->count(),"Record created incorrectly");

        // Try to add a record when we are authorised as a normal user - should succeed as long as the new werer
        // is associated with this user.
        $this->authorise_user();
        $uniqid = uniqid();
        $data = $this->makeTestData($uniqid);
        $data['user_id'] = 4;
        $this->post('/wearers/add.json', $data);
        //echo($this->_response);
        $this->assertResponseError("Add authorised POST request succeeded incorrectly (user)");
        $wearers = TableRegistry::getTableLocator()->get('Wearers');
        $query = $wearers->find()->where(['name' => $uniqid]);
        $this->assertEquals(0, $query->count(),"Record created incorrectly");

        $this->authorise_user();
        $uniqid = uniqid();
        $data = $this->makeTestData($uniqid);
        $data['user_id'] = 3;
        $this->post('/wearers/add.json', $data);
        //echo($this->_response);
        $this->assertResponseOK("Failed to add wearer (user)");
        $wearers = TableRegistry::getTableLocator()->get('Wearers');
        $query = $wearers->find()->where(['name' => $uniqid]);
        $this->assertEquals(1, $query->count(),"Record not created");
        
        // Try to add a record when we are authorised as an admin user - should succeed
        $this->authorise_admin();
        $uniqid = uniqid();
        $data = $this->makeTestData($uniqid);
        $this->post('/wearers/add.json', $data);
        //echo(print_r($this->_response));
        $this->assertResponseOK("Add admin POST request failed");
        $wearers = TableRegistry::getTableLocator()->get('Wearers');
        //echo("data");
        //echo(print_r($data));
        //$query = $wearers->find('all');
        //foreach ($query as $row)
        //    echo($row['uname'].", ");
        //echo(print_r($result));
        $query = $wearers->find()->where(['name' => $uniqid]);
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
        $this->get('/wearers/edit/1.json');
        $this->assertResponseError("Unauthorised view request succeeded incorrectly");

        $this->authorise_admin();
        $data=$this->makeTestData("user");
        $this->post('/wearers/edit/3.json',$data);
        $this->assertResponseOK("Authorised edit of own user record Failed (admin)");

        $this->authorise_user();
        $data=$this->makeTestData("user");
        $this->post('/wearers/edit/3.json',$data);
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
        $this->get('/wearers/delete/1.json');
        $this->assertResponseError("Unauthorised delete request succeeded incorrectly");

        $this->authorise_user();
        $this->post('/wearers/delete/3.json');
        $this->assertResponseOK("Authorised delete of own wearer record failed (user)");

        $this->authorise_analyst();
        $this->post('/wearers/delete/3.json');
        $this->assertResponseError("Authorised delete of other users wearer record succeeded incorrectly (analyst)");

        $this->authorise_admin();
        $this->post('/wearers/delete/2.json');
        $this->assertResponseOK("Authorised delete user record Failed (admin)");
    }
}
