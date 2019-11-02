<?php
namespace App\Test\TestCase\Model\Table;

use App\Model\Table\DatapointsTable;
use Cake\ORM\TableRegistry;
use Cake\TestSuite\TestCase;

/**
 * App\Model\Table\DatapointsTable Test Case
 */
class DatapointsTableTest extends TestCase
{
    /**
     * Test subject
     *
     * @var \App\Model\Table\DatapointsTable
     */
    public $Datapoints;

    /**
     * Fixtures
     *
     * @var array
     */
    public $fixtures = [
        'app.Datapoints',
        'app.Users',
        'app.Wearers',
        'app.Categories'
    ];

    /**
     * setUp method
     *
     * @return void
     */
    public function setUp()
    {
        parent::setUp();
        $config = TableRegistry::getTableLocator()->exists('Datapoints') ? [] : ['className' => DatapointsTable::class];
        $this->Datapoints = TableRegistry::getTableLocator()->get('Datapoints', $config);
    }

    /**
     * tearDown method
     *
     * @return void
     */
    public function tearDown()
    {
        unset($this->Datapoints);

        parent::tearDown();
    }

    /**
     * Test initialize method
     *
     * @return void
     */
    public function testInitialize()
    {
        $this->markTestIncomplete('Not implemented yet.');
    }

    /**
     * Test validationDefault method
     *
     * @return void
     */
    public function testValidationDefault()
    {
        $this->markTestIncomplete('Not implemented yet.');
    }

    /**
     * Test buildRules method
     *
     * @return void
     */
    public function testBuildRules()
    {
        $this->markTestIncomplete('Not implemented yet.');
    }
}
