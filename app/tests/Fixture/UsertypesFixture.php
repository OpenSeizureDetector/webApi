<?php
namespace App\Test\Fixture;

use Cake\TestSuite\Fixture\TestFixture;

/**
 * UsertypesFixture
 */
class UsertypesFixture extends TestFixture
{
    /**
     * Fields
     *
     * @var array
     */
    // @codingStandardsIgnoreStart
    public $fields = [
        'id' => ['type' => 'integer', 'length' => 11, 'unsigned' => false, 'null' => false, 'default' => null, 'comment' => '', 'autoIncrement' => true, 'precision' => null],
        'title' => ['type' => 'string', 'length' => 30, 'null' => true, 'default' => null, 'collate' => 'latin1_swedish_ci', 'comment' => '', 'precision' => null, 'fixed' => null],
        'description' => ['type' => 'string', 'length' => 512, 'null' => true, 'default' => null, 'collate' => 'latin1_swedish_ci', 'comment' => '', 'precision' => null, 'fixed' => null],
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
                'title' => 'Admin',
                'description' => 'Administrator',
                'created' => '2019-11-01 17:16:46',
                'modified' => '2019-11-01 17:16:46'
            ],
            [
                'id' => 2,
                'title' => 'Analyst',
                'description' => 'Analyst',
                'created' => '2019-11-01 17:16:46',
                'modified' => '2019-11-01 17:16:46'
            ],
            [
                'id' => 3,
                'title' => 'User',
                'description' => 'Normal User',
                'created' => '2019-11-01 17:16:46',
                'modified' => '2019-11-01 17:16:46'
            ],
        ];
        parent::init();
    }
}
