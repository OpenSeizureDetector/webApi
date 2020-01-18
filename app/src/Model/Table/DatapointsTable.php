<?php
namespace App\Model\Table;

use Cake\ORM\Query;
use Cake\ORM\RulesChecker;
use Cake\ORM\Table;
use Cake\Validation\Validator;

/**
 * Datapoints Model
 *
 * @property \App\Model\Table\UsersTable&\Cake\ORM\Association\BelongsTo $Users
 * @property \App\Model\Table\WearersTable&\Cake\ORM\Association\BelongsTo $Wearers
 * @property \App\Model\Table\CategoriesTable&\Cake\ORM\Association\BelongsTo $Categories
 *
 * @method \App\Model\Entity\Datapoint get($primaryKey, $options = [])
 * @method \App\Model\Entity\Datapoint newEntity($data = null, array $options = [])
 * @method \App\Model\Entity\Datapoint[] newEntities(array $data, array $options = [])
 * @method \App\Model\Entity\Datapoint|false save(\Cake\Datasource\EntityInterface $entity, $options = [])
 * @method \App\Model\Entity\Datapoint saveOrFail(\Cake\Datasource\EntityInterface $entity, $options = [])
 * @method \App\Model\Entity\Datapoint patchEntity(\Cake\Datasource\EntityInterface $entity, array $data, array $options = [])
 * @method \App\Model\Entity\Datapoint[] patchEntities($entities, array $data, array $options = [])
 * @method \App\Model\Entity\Datapoint findOrCreate($search, callable $callback = null, $options = [])
 *
 * @mixin \Cake\ORM\Behavior\TimestampBehavior
 */
class DatapointsTable extends Table
{
    /**
     * Initialize method
     *
     * @param array $config The configuration for the Table.
     * @return void
     */
    public function initialize(array $config)
    {
        parent::initialize($config);

        $this->setTable('datapoints');
        $this->setDisplayField('id');
        $this->setPrimaryKey('id');

        $this->addBehavior('Timestamp');

        $this->belongsTo('Users', [
            'foreignKey' => 'user_id',
            'joinType' => 'INNER'
        ]);
        $this->belongsTo('Wearers', [
            'foreignKey' => 'wearer_id',
            'joinType' => 'INNER'
        ]);
        $this->belongsTo('Categories', [
            'foreignKey' => 'category_id'
        ]);
    }

    /**
     * Default validation rules.
     *
     * @param \Cake\Validation\Validator $validator Validator instance.
     * @return \Cake\Validation\Validator
     */
    public function validationDefault(Validator $validator)
    {
        $validator
            ->integer('id')
            ->allowEmptyString('id', null, 'create');

        $validator
            ->dateTime('dataTime')
            ->allowEmptyDateTime('dataTime');

        $validator
            ->numeric('accMean')
            ->allowEmptyString('accMean');

        $validator
            ->numeric('accSd')
            ->allowEmptyString('accSd');

        $validator
            ->numeric('hr')
            ->allowEmptyString('hr');

        $validator
            ->scalar('dataJSON')
            ->allowEmptyString('dataJSON');

        return $validator;
    }

    /**
     * Returns a rules checker object that will be used for validating
     * application integrity.
     *
     * @param \Cake\ORM\RulesChecker $rules The rules object to be modified.
     * @return \Cake\ORM\RulesChecker
     */
    public function buildRules(RulesChecker $rules)
    {
        $rules->add($rules->existsIn(['user_id'], 'Users'));
        $rules->add($rules->existsIn(['wearer_id'], 'Wearers'));
        $rules->add($rules->existsIn(['category_id'], 'Categories'));

        return $rules;
    }



    // FIXME - this doesn't work when placed here!!!
    public function addDatapoint($data = array()) {
        $datapoint = $this->Datapoints->newEntity();
        $this->Authorization->authorize($datapoint,'create');
        
        // Interpret the data that has been sent into the correct format.
        $data = $this->request->getData();
        //echo("data=".$data);
        
        $patchdata = array();
        $user = $this->Authentication->getIdentity()->getIdentifier();
        $patchdata['user_id'] = $user;
        $patchdata['wearer_id'] = 1;
        $patchdata['dataJSON'] = json_encode($data);
        $patchdata['dataTime'] = date('Y-m-d H:i:s', strtotime($data['dateStr'])); 
        
        $accSum = 0.0;
        $nData = 0;
        if (count($data['rawData'])>0) {
            foreach ($data['rawData'] as $val) {
        	    $accSum += $val;
                $nData += 1;
            }
        }
        if ($nData<>0) {
            $accMean = $accSum/$nData;
        } else {
            $accMean = 0.;
        }
        $patchdata['accMean'] = $accMean;
        
        $devSq = 0;
        foreach ($data['rawData'] as $val) {
            $devSq += pow($val - $accMean, 2);
        }
        if ($nData<>0) {
            $patchdata['accSd'] = (float)sqrt($devSq/$nData);
        } else {
            $patchdata['accSd'] = 0.0;
        }
        $patchdata['hr'] = $data['hr'];
        
        debug($patchdata,false);
        $datapoint = $this->Datapoints->patchEntity($datapoint, $patchdata);
        
        if ($this->Datapoints->save($datapoint)) {
            return($datapoint);
        } else {
            return(null);
        }
    }
    
}
