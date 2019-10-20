<?php
// src/Model/Entity/Category.php
namespace App\Model\Entity;

use Cake\ORM\Entity;

class Category extends Entity
{
    protected $_accessible = [
        '*' => true,
        'id' => false
    ];
}