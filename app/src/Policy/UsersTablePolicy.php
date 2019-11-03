<?php
namespace App\Policy;

use App\Model\Table\DatapointsTable;
use Authorization\IdentityInterface;

/**
 * Datapoints policy
 */
class UsersTablePolicy
{
    public function scopeIndex($user, $query)
    {
        // Only admin can list all users
        if ($user->usertype_id != 1)
            return $query->where(['Users.id' => $user->id]);
        else
            return $query;
    }
}
