<?php
namespace App\Policy;

use App\Model\Entity\User;
use Authorization\IdentityInterface;

class UserPolicy
{
    const USERTYPE_ADMIN = 1;
    const USERTYPE_ANALYST = 2;
    /**
     * Check if $user can create User
     *
     * @param Authorization\IdentityInterface $user The user.
     * @param App\Model\Entity\User $userquery
     * @return bool
     */
    public function canCreate(IdentityInterface $user, User $userquery)
    {
        // Anyone can create a user
        return true;
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
        // only the user can do it
        if ($user->id == $userquery->user_id)
            $allowed = true;
        if ($user->usertype_id == self::USERTYPE_ADMIN)
            $allowed = true;
        echo(print_r($user));
        return $allowed;
    }

    public function canSetCategory(IdentityInterface $user, User $userquery) {
        return $this->canUpdate($user, $userquery);
    }

    public function canEdit(IdentityInterface $user, User $userquery) {
        return $this->canUpdate($user, $userquery);
    }
    
    /**
     * Check if $user can delete User
     *
     * @param Authorization\IdentityInterface $user The user.
     * @param App\Model\Entity\User $userquery
     * @return bool
     */
    public function canDelete(IdentityInterface $user, User $userquery)
    {
        return $this->canUpdate($user, $userquery);
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
        // only the user can do it
        if ($user->id == $userquery->id)
            $allowed = true;
        if ($user->usertype_id == self::USERTYPE_ANALYST)
            $allowed = true;
        if ($user->usertype_id == self::USERTYPE_ADMIN)
            $allowed = true;
        //echo(print_r($user));
        return $allowed;
    }
}
