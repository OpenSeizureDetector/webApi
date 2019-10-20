<!-- File: src/Template/DataPoints/index.ctp -->

<h1>DataPoints</h1>
<table>
    <tr>
        <th>Time</th>
        <th>Hr</th>
    </tr>

    <?php foreach ($datapoints as $dp): ?>
    <tr>
        <td>
            <?= $dp->dataTime->format(DATE_RFC850) ?>
        </td>
        <td>
            <?= $dp->hr ?>
        </td>
    </tr>
    <?php endforeach; ?>
</table>