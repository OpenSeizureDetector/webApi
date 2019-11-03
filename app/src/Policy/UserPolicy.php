<?php
namespace App\Policy;

use App\Model\Entity\User;
use Authorization\IdentityInterface;

class UserPolicy
{
    const USERTYPE_ADMIN = 1;
    const USERTYPE_ANALYST = 2;

    public function canCreate(IdentityInterface $user, User $userquery)
    {
        $allowed = false;
        // only admin can create users
        if ($user->usertype_id == self::USERTYPE_ADMIN)
            $allowed = true;
        return $allowed;

    }

    /**
     * Check if $user can update User
     *
     * @param Authorization\IdentityInterface $user The user.
     * @param App\Model\Entity\User $userquery
     * @return bool
     */
    public function canUpdate(IdentityInterface $user, User $userquery)
    {
        $allowed = false;
        // only the user or admin can do it
        //echo("canUpdate: identity userID=".$user->id.", query user_id=".$userquery->id.".");
        if ($user->id == $userquery->id)
            $allowed = true;
        if ($user->usertype_id == self::USERTYPE_ADMIN)
            $allowed = true;
        //echo(print_r($user));
        return $allowed;
    }

    public function canEdit(IdentityInterface $user, User $userquery) {
        return $this->canUpdate($user, $userquery);
    }
    
    public function canDelete(IdentityInterface $user, User $userquery)
    {
        $allowed = false;
        // only admin can do it
        //echo("canUpdate: identity userID=".$user->id.", query user_id=".$userquery->id.".");
        if ($user->usertype_id == self::USERTYPE_ADMIN)
            $allowed = true;
        //echo(print_r($user));
        return $allowed;
    }

    /**
     * Check if $user can view User
     *
     * @param Authorization\IdentityInterface $user The user.
     * @param App\Model\Entity\User $userquery
     * @return bool
     */
    public function canView(IdentityInterface $user, User $userquery)
    {
        $allowed = false;
        if ($user->usertype_id == self::USERTYPE_ADMIN)
            $allowed = true;
        if ($user->id == $userquery->id)
            $allowed = true;
        return $allowed;
    }
}
