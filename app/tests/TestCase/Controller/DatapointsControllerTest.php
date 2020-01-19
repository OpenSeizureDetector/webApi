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
    
    public function testIndex()
    {
        $this->unauthorise();
        $this->get('/datapoints.json');
        $this->assertResponseError("Unauthorised request succeeded incorrectly");
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


    
    public function testView()
    {
        $this->unauthorise();
        $this->get('/datapoints/view/1.json');
        $this->assertResponseError("Unauthorised view request succeeded incorrectly");

        $this->authorise_user();
        $this->get('/datapoints/view/3.json');
        $this->assertResponseOK("Authorised view of own datapoint Failed (user)");

        $this->authorise_user();
        $this->get('/datapoints/view/4.json');
        $this->assertResponseError("Authorised view of other users' datapoint succeeded incorrectly (user)");

        $this->authorise_analyst();
        $this->get('/datapoints/view/3.json');
        $this->assertResponseOK("Authorised view of other users datapoint datapoint Failed (analyst)");

        $this->authorise_admin();
        $this->get('/datapoints/view/3.json');
        $this->assertResponseOK("Authorised view of other users datapoint datapoint Failed (admin)");
    }


    private function makeTestData($uniqid,$userType) {
        $data = [
                'dateStr' => '2019-10-20 10:28:26',
                'user_id' => 1,
                'wearerId' => 1,
                'accMean' => 1000.,
                'accSd' => 100.,
                'hr' => 70.,
                'category_id' => 1,
                'dataJSON' => $uniqid,
                'rawData' => [1224.0, 1248.0, 1248.0, 1240.0, 1232.0, 1240.0, 1236.0, 1244.0, 1220.0, 1236.0, 1240.0, 1240.0, 1216.0, 1236.0, 1232.0, 1232.0, 1228.0, 1248.0, 1224.0, 1220.0, 1224.0, 1236.0, 1240.0, 1220.0, 1236.0, 1240.0, 1236.0, 1224.0, 1244.0, 1236.0, 1248.0, 1228.0, 1228.0, 1236.0, 1244.0, 1252.0, 1236.0, 1240.0, 1236.0, 1240.0, 1220.0, 1248.0, 1236.0, 1220.0, 1236.0, 1236.0, 1220.0, 1236.0, 1236.0, 1232.0, 1212.0, 1244.0, 1244.0, 1236.0, 1224.0, 1228.0, 1240.0, 1240.0, 1240.0, 1240.0, 1232.0, 1228.0, 1248.0, 1244.0, 1232.0, 1228.0, 1236.0, 1256.0, 1228.0, 1212.0, 1228.0, 1224.0, 1236.0, 1232.0, 1232.0, 1232.0, 1220.0, 1240.0, 1224.0, 1228.0, 1232.0, 1240.0, 1236.0, 1228.0, 1232.0, 1232.0, 1228.0, 1224.0, 1244.0, 1236.0, 1228.0, 1220.0, 1224.0, 1224.0, 1228.0, 1216.0, 1244.0, 1240.0, 1248.0, 1224.0, 1216.0, 1228.0, 1240.0, 1224.0, 1220.0, 1224.0, 1216.0, 1244.0, 1236.0, 1240.0, 1240.0, 1252.0, 1232.0, 1224.0, 1236.0, 1228.0, 1216.0, 1248.0, 1220.0, 1232.0, 1244.0, 1244.0, 1224.0, 1228.0, 1232.0],
                'created' => '2019-10-20 10:28:26',
                'modified' => '2019-10-20 10:28:26'
        ];

        // admin user
        if ($userType == 1) {
            $data['user_id']=1;
            $data['wearerId']=1;
        }

        // analyst user
        if ($userType == 2) {
            $data['user_id']=2;
            $data['wearerId']=5;

        }
        // normal user
        if ($userType == 3) {
            $data['user_id']=3;
            $data['wearerId']=1;

        }
        
        return $data;
    }
    
    public function testAdd()
    {
        // Try to add a record when we are unauthorised
        $this->unauthorise();
        $uniqid = uniqid();
        $data = $this->makeTestData($uniqid,1);
        $this->post('/datapoints/add.json', $data);
        $this->assertResponseError("Add unauthorised POST request succeeded incorrectly");
        $datapoints = TableRegistry::getTableLocator()->get('Datapoints');
        $query = $datapoints->find()->where(['dataJSON' => $uniqid]);
        $this->assertEquals(0, $query->count(),"Record created incorrectly");

        // Try to add a record when we are authorised as a normal user
        $this->authorise_user();
        $uniqid = uniqid();
        $data = $this->makeTestData($uniqid,3);
        $datapoints = TableRegistry::getTableLocator()->get('Datapoints');
        $startCount = $datapoints->find()->count();
        $this->post('/datapoints/add.json', $data);
        $this->assertResponseOK("Add authorised POST request failed (user)");
        $query = $datapoints->find()->where(['dataJSON' => $uniqid]);
        $endCount = $datapoints->find()->count();
        $this->assertEquals(1, $endCount-$startCount,"Record created ok");

        // Try to add a record for another users wearer we are authorised as a normal user
        $this->authorise_user();
        $uniqid = uniqid();
        $data = $this->makeTestData($uniqid,3);
        $data['wearerId'] = 4;
        $datapoints = TableRegistry::getTableLocator()->get('Datapoints');
        $startCount = $datapoints->find()->count();
        $this->post('/datapoints/add.json', $data);
        $this->assertResponseError("Add authorised POST request failed (user)");
        $query = $datapoints->find()->where(['dataJSON' => $uniqid]);
        $endCount = $datapoints->find()->count();
        $this->assertEquals(0, $endCount-$startCount,"Record created ok");

        // Try to add a record for our own wearer when we are authorised as an analyst
        $this->authorise_analyst();
        $uniqid = uniqid();
        $data = $this->makeTestData($uniqid,2);
        $datapoints = TableRegistry::getTableLocator()->get('Datapoints');
        $startCount = $datapoints->find()->count();
        $this->post('/datapoints/add.json', $data);
        $this->assertResponseOK("Add authorised POST request failed (analyst)");
        $query = $datapoints->find()->where(['dataJSON' => $uniqid]);
        $endCount = $datapoints->find()->count();
        $this->assertEquals(1, $endCount-$startCount,"Record created ok");

        // Try to add a record for another user's wearere when we are authorised as an analyst
        $this->authorise_analyst();
        $uniqid = uniqid();
        $data = $this->makeTestData($uniqid,2);
        $data['wearerId']=1;   //  Wearer 1 is owned by user 1 in WearersFixture.
        $datapoints = TableRegistry::getTableLocator()->get('Datapoints');
        $startCount = $datapoints->find()->count();
        $this->post('/datapoints/add.json', $data);
        $this->assertResponseError("Add authorised POST request failed (analyst)");
        $query = $datapoints->find()->where(['dataJSON' => $uniqid]);
        $endCount = $datapoints->find()->count();
        $this->assertEquals(0, $endCount-$startCount,"Record created ok");

        
        // Try to add a record when we are authorised as admin
        $this->authorise_admin();
        $uniqid = uniqid();
        $data = $this->makeTestData($uniqid,1);
        $datapoints = TableRegistry::getTableLocator()->get('Datapoints');
        $startCount = $datapoints->find()->count();
        $this->post('/datapoints/add.json', $data);
        $this->assertResponseOK("Add authorised POST request failed (admin)");
        $query = $datapoints->find()->where(['dataJSON' => $uniqid]);
        $endCount = $datapoints->find()->count();
        $this->assertEquals(1, $endCount-$startCount,"Record created ok");
        
        // Try to add a record for another user's wearer when we are authorised as admin
        $this->authorise_admin();
        $uniqid = uniqid();
        $data = $this->makeTestData($uniqid,1);
        $data['wearerId'] = 1;   // wearer 1 is owned by user 3 in WearersFixture
        $datapoints = TableRegistry::getTableLocator()->get('Datapoints');
        $startCount = $datapoints->find()->count();
        $this->post('/datapoints/add.json', $data);
        $this->assertResponseOK("Add authorised POST request failed (admin)");
        $query = $datapoints->find()->where(['dataJSON' => $uniqid]);
        $endCount = $datapoints->find()->count();
        $this->assertEquals(1, $endCount-$startCount,"Record created ok");
    }



    public function testSetCategoryUnauthorised()
    {
        $this->get('/datapoints/setCategory/1/1.json');
        $this->assertResponseError("changed category incorrectly when unauthorised");
    }


}
