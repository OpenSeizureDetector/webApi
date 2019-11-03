<?php
namespace App\Policy;

//use App\Model\Table\DatapointsTable;
use Authorization\IdentityInterface;

class WearersTablePolicy
{
    public function scopeIndex($user, $query)
    {
        // Only admin can list all wearers
        if ($user->usertype_id != 1)
            return $query->where(['Wearers.user_id' => $user->id]);
        else
            return $query;
    }
}
