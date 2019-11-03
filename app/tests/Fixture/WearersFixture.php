<?php
namespace App\Test\Fixture;

use Cake\TestSuite\Fixture\TestFixture;

/**
 * WearersFixture
 */
class WearersFixture extends TestFixture
{
    /**
     * Fields
     *
     * @var array
     */
    // @codingStandardsIgnoreStart
    public $fields = [
        'id' => ['type' => 'integer', 'length' => 11, 'unsigned' => false, 'null' => false, 'default' => null, 'comment' => '', 'autoIncrement' => true, 'precision' => null],
        'name' => ['type' => 'string', 'length' => 255, 'null' => false, 'default' => null, 'collate' => 'latin1_swedish_ci', 'comment' => '', 'precision' => null, 'fixed' => null],
        'dob' => ['type' => 'date', 'length' => null, 'null' => true, 'default' => null, 'comment' => '', 'precision' => null],
        'ald' => ['type' => 'boolean', 'length' => null, 'null' => true, 'default' => null, 'comment' => '', 'precision' => null],
        'user_id' => ['type' => 'integer', 'length' => 11, 'unsigned' => false, 'null' => false, 'default' => null, 'comment' => '', 'precision' => null, 'autoIncrement' => null],
        'created' => ['type' => 'datetime', 'length' => null, 'null' => true, 'default' => null, 'comment' => '', 'precision' => null],
        'modified' => ['type' => 'datetime', 'length' => null, 'null' => true, 'default' => null, 'comment' => '', 'precision' => null],
        '_constraints' => [
            'primary' => ['type' => 'primary', 'columns' => ['id'], 'length' => []],
        ],
        '_options' => [
            'engine' => 'InnoDB',
            'collation' => 'latin1_swedish_ci'
        ],
    ];
    // @codingStandardsIgnoreEnd
    /**
     * Init method
     *
     * @return void
     */
    public function init()
    {
        $this->records = [
            [
                'id' => 1,
                'name' => 'Wearer_1',
                'dob' => '2019-11-02',
                'ald' => 1,
                'user_id' => 3,
                'created' => '2019-11-02 19:29:58',
                'modified' => '2019-11-02 19:29:58'
            ],
            [
                'id' => 2,
                'name' => 'Wearer_2',
                'dob' => '2019-11-02',
                'ald' => 1,
                'user_id' => 3,
                'created' => '2019-11-02 19:29:58',
                'modified' => '2019-11-02 19:29:58'
            ],
            [
                'id' => 3,
                'name' => 'Wearer_3',
                'dob' => '2019-11-02',
                'ald' => 0,
                'user_id' => 3,
                'created' => '2019-11-02 19:29:58',
                'modified' => '2019-11-02 19:29:58'
            ],
            [
                'id' => 4,
                'name' => 'Wearer_4',
                'dob' => '2019-11-02',
                'ald' => 0,
                'user_id' => 4,
                'created' => '2019-11-02 19:29:58',
                'modified' => '2019-11-02 19:29:58'
            ],
        ];
        parent::init();
    }
}
