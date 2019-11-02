<?php
namespace App\Test\TestCase\Controller;

use App\Controller\DatapointsController;
use Cake\TestSuite\IntegrationTestTrait;
use Cake\TestSuite\TestCase;
use Cake\ORM\TableRegistry;

/**
 * App\Controller\DatapointsController Test Case
 *
 * @uses \App\Controller\DatapointsController
 */
class DatapointsControllerTest extends TestCase
{
    use IntegrationTestTrait;

    public $fixtures = [
        'app.Datapoints', 'app.Users', 'app.Wearers', 'app.Categories'
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
    
    public function testIndexUnauthorised()
    {
        $this->unauthorise();
        $this->get('/datapoints.json');
        $this->assertResponseError("Unauthorised request succeeded incorrectly");
    }

    public function testIndexAuthorised()
    {
        $this->authorise_admin();
        $this->get('/datapoints.json');
        $this->assertResponseOK("Authorised Request Failed (Admin)");
        $this->authorise_analyst();
        $this->get('/datapoints.json');
        $this->assertResponseOK("Authorised Request Failed (analyst)");
        $this->authorise_user();
        $this->get('/datapoints.json');
        $this->assertResponseOK("Authorised Request Failed (user)");

    }


    
    public function testViewUnauthorised()
    {
        $this->unauthorise();
        $this->get('/datapoints/view/1.json');
        $this->assertResponseCode(401,"Unauthorised view request succeeded incorrectly");
    }


    public function testAddUnauthorised()
    {
        $this->unauthorise();
        $uniqid = uniqid();
        $data = [
                'dataTime' => '2019-10-20 10:28:26',
                'user_id' => 1,
                'wearer_id' => 1,
                'accMean' => 1000.,
                'accSd' => 100.,
                'hr' => 70.,
                'category_id' => 1,
                'dataJSON' => $uniqid,
                'created' => '2019-10-20 10:28:26',
                'modified' => '2019-10-20 10:28:26'
        ];

        $this->post('/datapoints/add.json', $data);

        $this->assertResponseError(401,"Add unauthorised POST request succeeded incorrectly");
	
        $datapoints = TableRegistry::getTableLocator()->get('Datapoints');
        $query = $datapoints->find()->where(['dataJSON' => $uniqid]);
        $this->assertEquals(0, $query->count(),"Record created incorrectly");
    }

    public function testAddAuthorised()
    {
        $this->authorise();
        $uniqid = uniqid();
        $data = [
                'dataTime' => '2019-10-20 10:28:26',
                'user_id' => 1,
                'wearer_id' => 1,
                'accMean' => 1000.,
                'accSd' => 100.,
                'hr' => 70.,
                'category_id' => 1,
                'dataJSON' => $uniqid,
                'created' => '2019-10-20 10:28:26',
                'modified' => '2019-10-20 10:28:26'
        ];

        $this->post('/datapoints/add.json', $data);

        $this->assertResponseOK(401,"Authorised Add POST request failed");
	
        $datapoints = TableRegistry::getTableLocator()->get('Datapoints');
        $query = $datapoints->find()->where(['dataJSON' => $uniqid]);
        $this->assertEquals(1, $query->count(),"We do not have one record with uniquid");
    }



    public function testSetCategoryUnauthorised()
    {
        $this->get('/datapoints/setCategory/1/1.json');
        $this->assertResponseError("changed category incorrectly when unauthorised");
    }


}
