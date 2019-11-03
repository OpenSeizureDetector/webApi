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

    /**
     * Test add method
     *
     * @return void
     */
    public function testAdd()
    {
        $this->markTestIncomplete('Not implemented yet.');
    }

    /**
     * Test edit method
     *
     * @return void
     */
    public function testEdit()
    {
        $this->markTestIncomplete('Not implemented yet.');
    }

    /**
     * Test delete method
     *
     * @return void
     */
    public function testDelete()
    {
        $this->markTestIncomplete('Not implemented yet.');
    }
}
