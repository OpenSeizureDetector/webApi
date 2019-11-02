<?php
namespace App\Policy;

use App\Model\Table\DatapointsTable;
use Authorization\IdentityInterface;

/**
 * Datapoints policy
 */
class DatapointsTablePolicy
{
    public function scopeIndex($user, $query)
    {
        if ($user->usertype_id == 3)
            return $query->where(['Datapoints.user_id' => $user->id]);
        else
            return $query;
    }
}
