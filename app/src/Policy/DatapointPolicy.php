<?php
namespace App\Policy;

use App\Model\Entity\datapoint;
use Authorization\IdentityInterface;

/**
 * datapoint policy
 */
class datapointPolicy
{
    /**
     * Check if $user can create datapoint
     *
     * @param Authorization\IdentityInterface $user The user.
     * @param App\Model\Entity\datapoint $datapoint
     * @return bool
     */
    public function canCreate(IdentityInterface $user, datapoint $datapoint)
    {
    }

    /**
     * Check if $user can update datapoint
     *
     * @param Authorization\IdentityInterface $user The user.
     * @param App\Model\Entity\datapoint $datapoint
     * @return bool
     */
    public function canUpdate(IdentityInterface $user, datapoint $datapoint)
    {
    }

    /**
     * Check if $user can delete datapoint
     *
     * @param Authorization\IdentityInterface $user The user.
     * @param App\Model\Entity\datapoint $datapoint
     * @return bool
     */
    public function canDelete(IdentityInterface $user, datapoint $datapoint)
    {
    }

    /**
     * Check if $user can view datapoint
     *
     * @param Authorization\IdentityInterface $user The user.
     * @param App\Model\Entity\datapoint $datapoint
     * @return bool
     */
    public function canView(IdentityInterface $user, datapoint $datapoint)
    {
        return true;
    }
}
