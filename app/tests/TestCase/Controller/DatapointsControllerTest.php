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
        'app.Datapoints'
    ];

    public function testIndexUnauthorised()
    {
        $this->get('/datapoints.json');
        $this->assertResponseCode(401,"Unauthorised request succeeded incorrectly");
    }

    public function testIndexAuthorised()
    {
        $this->configRequest([
            'environment' => [
                'PHP_AUTH_USER' => 'admin',
                'PHP_AUTH_PW' => 'admin_pw',
            ]
        ]);
        $this->get('/datapoints.json');
        $this->assertResponseCode(401,"Authorised Request Failed");
    }


    
    public function testViewUnauthorised()
    {
        $this->get('/datapoints/view/1.json');
        $this->assertResponseCode(401,"Unauthorised view request succeeded incorrectly");
    }


    public function testAddUnauthorised()
    {
        $data = [
                'dataTime' => '2019-10-20 10:28:26',
                'user_id' => 1,
                'wearer_id' => 1,
                'accMean' => 1000.,
                'accSd' => 100.,
                'hr' => 70.,
                'category_id' => 1,
                'dataJSON' => 'test dataJSON',
                'created' => '2019-10-20 10:28:26',
                'modified' => '2019-10-20 10:28:26'
        ];

        $this->post('/datapoints/add.json', $data);

        $this->assertResponseCode(401,"Add POST request failed");
	
        $datapoints = TableRegistry::getTableLocator()->get('Datapoints');
        $query = $datapoints->find()->where(['dataTime' => $data['dataTime']]);
        $this->assertEquals(1, $query->count(),"More than 1 record with same dataTime");
    }



    public function testSetCategoryUnauthorised()
    {
        $this->get('/datapoints/setCategory/1/1.json');
        $this->assertResponseCode(401);
    }


}
