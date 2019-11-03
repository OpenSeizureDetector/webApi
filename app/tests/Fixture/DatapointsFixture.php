<?php
namespace App\Test\Fixture;

use Cake\TestSuite\Fixture\TestFixture;

/**
 * DatapointsFixture
 */
class DatapointsFixture extends TestFixture
{
    public $import = ['table' => 'datapoints'];
    public function init()
    {
        $this->records = [
            [
                'id' => 1,
                'dataTime' => '2019-10-20 10:28:26',
                'user_id' => 3, 'wearer_id' => 1,
                'accMean' => 1, 'accSd' => 1, 'hr' => 1,
                'category_id' => 1,
                'dataJSON' => 'rec1',
                'created' => '2019-10-20 10:28:26',
                'modified' => '2019-10-20 10:28:26'
            ],
            [
                'id' => 2,
                'dataTime' => '2019-10-20 10:28:26',
                'user_id' => 3, 'wearer_id' => 1,
                'accMean' => 1, 'accSd' => 1, 'hr' => 1,
                'category_id' => 1,
                'dataJSON' => 'rec2',
                'created' => '2019-10-20 10:28:26',
                'modified' => '2019-10-20 10:28:26'
            ],
            [
                'id' => 3,
                'dataTime' => '2019-10-20 10:28:26',
                'user_id' => 3, 'wearer_id' => 1,
                'accMean' => 1, 'accSd' => 1, 'hr' => 1,
                'category_id' => 1,
                'dataJSON' => 'rec3',
                'created' => '2019-10-20 10:28:26',
                'modified' => '2019-10-20 10:28:26'
            ],
            [
                'id' => 4,
                'dataTime' => '2019-10-20 10:28:26',
                'user_id' => 4, 'wearer_id' => 1,
                'accMean' => 1, 'accSd' => 1, 'hr' => 1,
                'category_id' => 1,
                'dataJSON' => 'rec4',
                'created' => '2019-10-20 10:28:26',
                'modified' => '2019-10-20 10:28:26'
            ],
        ];
        parent::init();
    }
}
