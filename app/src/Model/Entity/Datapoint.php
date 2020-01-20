<?php
namespace App\Model\Entity;

use Cake\ORM\Entity;

/**
 * Datapoint Entity
 *
 * @property int $id
 * @property \Cake\I18n\FrozenTime|null $dataTime
 * @property int $user_id
 * @property int $wearer_id
 * @property float|null $accMean
 * @property float|null $accSd
 * @property float|null $hr
 * @property int|null $category_id
 * @property string|null $dataJSON
 * @property \Cake\I18n\FrozenTime|null $created
 * @property \Cake\I18n\FrozenTime|null $modified
 *
 * @property \App\Model\Entity\User $user
 * @property \App\Model\Entity\Wearer $wearer
 * @property \App\Model\Entity\Category $category
 */
class Datapoint extends Entity
{
    /**
     * Fields that can be mass assigned using newEntity() or patchEntity().
     *
     * Note that when '*' is set to true, this allows all unspecified fields to
     * be mass assigned. For security purposes, it is advised to set '*' to false
     * (or remove it), and explicitly make individual fields accessible as needed.
     *
     * @var array
     */
    protected $_accessible = [
        'dataTime' => true,
        'user_id' => true,
        'wearer_id' => true,
        'accMean' => true,
        'accSd' => true,
        'hr' => true,
        'category_id' => true,
        'dataJSON' => true,
        'created' => true,
        'modified' => true,
        'user' => true,
        'wearer' => true,
        'category' => true
    ];



}
