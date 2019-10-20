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

    /**
     * Fixtures
     *
     * @var array
     */
    public $fixtures = [
        'app.Datapoints'
    ];

    /**
     * Test index method
     *
     * @return void
     */
    public function testIndex()
    {
        $this->get('/datapoints.json');
        $this->assertResponseOk("Index request failed");
    }

    /**
     * Test view method
     *
     * @return void
     */
    public function testView()
    {
        $this->get('/datapoints/view/1.json');
        $this->assertResponseOk("View request failed");
    }


    public function testAdd()
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

        $this->assertResponseSuccess("Add POST request failed");
	
        $datapoints = TableRegistry::getTableLocator()->get('Datapoints');
        $query = $datapoints->find()->where(['dataTime' => $data['dataTime']]);
        $this->assertEquals(1, $query->count(),"More than 1 record with same dataTime");
    }



    public function testSetCategory()
    {
        $this->get('/datapoints/setCategory/1/1.json');
        $this->assertResponseOk("setCategory request failed");
    }


}
