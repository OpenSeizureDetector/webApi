<?php
namespace App\Policy;

use App\Model\Entity\datapoints;
use Authorization\IdentityInterface;

/**
 * datapoints policy
 */
class datapointsPolicy
{
    /**
     * Check if $user can create datapoints
     *
     * @param Authorization\IdentityInterface $user The user.
     * @param App\Model\Entity\datapoints $datapoints
     * @return bool
     */
    public function canCreate(IdentityInterface $user, datapoints $datapoints)
    {
    }

    /**
     * Check if $user can update datapoints
     *
     * @param Authorization\IdentityInterface $user The user.
     * @param App\Model\Entity\datapoints $datapoints
     * @return bool
     */
    public function canUpdate(IdentityInterface $user, datapoints $datapoints)
    {
    }

    /**
     * Check if $user can delete datapoints
     *
     * @param Authorization\IdentityInterface $user The user.
     * @param App\Model\Entity\datapoints $datapoints
     * @return bool
     */
    public function canDelete(IdentityInterface $user, datapoints $datapoints)
    {
    }

    /**
     * Check if $user can view datapoints
     *
     * @param Authorization\IdentityInterface $user The user.
     * @param App\Model\Entity\datapoints $datapoints
     * @return bool
     */
    public function canView(IdentityInterface $user, datapoints $datapoints)
    {
    }
}
