<?php
namespace App\Policy;

use App\Model\Entity\Datapoint;
use Authorization\IdentityInterface;

/**
 * Datapoint policy
 */
class DatapointPolicy
{
    const USERTYPE_ADMIN = 1;
    const USERTYPE_ANALYST = 2;
    /**
     * Check if $user can create Datapoint
     *
     * @param Authorization\IdentityInterface $user The user.
     * @param App\Model\Entity\Datapoint $datapoint
     * @return bool
     */
    public function canCreate(IdentityInterface $user, Datapoint $datapoint)
    {
        // Anyone can create a datapoint
        return true;
    }

    /**
     * Check if $user can update Datapoint
     *
     * @param Authorization\IdentityInterface $user The user.
     * @param App\Model\Entity\Datapoint $datapoint
     * @return bool
     */
    public function canUpdate(IdentityInterface $user, Datapoint $datapoint)
    {
        $allowed = false;
        // only the user can do it
        if ($user->id == $datapoint->user_id)
            $allowed = true;
        if ($user->usertype_id == self::USERTYPE_ADMIN)
            $allowed = true;
        echo(print_r($user));
        return $allowed;
    }

    public function canSetCategory(IdentityInterface $user, Datapoint $datapoint) {
        return $this->canUpdate($user, $datapoint);
    }

    public function canEdit(IdentityInterface $user, Datapoint $datapoint) {
        return $this->canUpdate($user, $datapoint);
    }
    
    /**
     * Check if $user can delete Datapoint
     *
     * @param Authorization\IdentityInterface $user The user.
     * @param App\Model\Entity\Datapoint $datapoint
     * @return bool
     */
    public function canDelete(IdentityInterface $user, Datapoint $datapoint)
    {
        return $this->canUpdate($user, $datapoint);
    }

    /**
     * Check if $user can view Datapoint
     *
     * @param Authorization\IdentityInterface $user The user.
     * @param App\Model\Entity\Datapoint $datapoint
     * @return bool
     */
    public function canView(IdentityInterface $user, Datapoint $datapoint)
    {
        $allowed = false;
        // only the user can do it
        if ($user->id == $datapoint->user_id)
            $allowed = true;
        if ($user->usertype_id == self::USERTYPE_ADMIN)
            $allowed = true;
        //echo(print_r($user));
        return $allowed;
    }
}
