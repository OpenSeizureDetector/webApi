<?php
namespace App\Model\Entity;
use Cake\Auth\DefaultPasswordHasher;

use Cake\ORM\Entity;

/**
 * User Entity
 *
 * @property int $id
 * @property string $uname
 * @property string|null $email
 * @property string $password
 * @property int $usertype_id
 * @property \Cake\I18n\FrozenTime|null $created
 * @property \Cake\I18n\FrozenTime|null $modified
 *
 * @property \App\Model\Entity\Usertype $usertype
 * @property \App\Model\Entity\Datapoint[] $datapoints
 */
class User extends Entity
{
    /**
     * Fields that can be mass assigned using newEntity() or patchEntity().
     */
    protected $_accessible = [
        'uname' => true,
        'email' => true,
        'password' => true,
        'usertype_id' => true,
        'created' => true,
        'modified' => true,
        'usertype' => true,
        'datapoints' => true
    ];

    /**
     * Fields that are excluded from JSON versions of the entity.
     *
     * @var array
     */
    protected $_hidden = [
        'password'
    ];


    protected function _setPassword($value)
    {
        if (strlen($value)) {
            $hasher = new DefaultPasswordHasher();

            return $hasher->hash($value);
        }
    }

}
